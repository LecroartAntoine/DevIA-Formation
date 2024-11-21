import React, { useState } from 'react';
import { Row, Col, Button, FormGroup, Label, ListGroup, ListGroupItem, Input } from 'reactstrap';
import { useForm } from 'react-hook-form';
import Form from 'react-validation/build/form';
import BreadCrumbs from '../../layouts/breadcrumbs/BreadCrumbs';

import ComponentCard from '../../components/ComponentCard';

const FormValidate = () => {
  const { register, handleSubmit, errors } = useForm(); // initialise the hook
  const [Formvalue, setFormvalue] = useState({
    firstname: '',
    lastname: '',
    email: '',
    age: '',
    title: '',
    mobile: '',
    developer: '',
  });
  const onSubmit = (data) => {
    setFormvalue(data);
  };
  return (
    <>
      <BreadCrumbs />
      <Row>
        <Col sm="12">
          <ComponentCard title="Form Validation">
            <Form onSubmit={handleSubmit(onSubmit)}>
              <FormGroup>
                <Label className="control-Label" htmlFor="firstname">
                  First name *
                </Label>
                <div className="mb-2">
                  <input
                    type="text"
                    name="firstname"
                    ref={register({ required: true })}
                    className="form-control"
                  />
                </div>
                <span className="text-danger">{errors.firstname && 'First name is required.'}</span>
              </FormGroup>
              <FormGroup>
                <Label className="control-Label" htmlFor="lastname">
                  Last name *
                </Label>
                <div className="mb-2">
                  <input
                    type="text"
                    name="lastname"
                    ref={register({ required: true })}
                    className="form-control"
                  />
                </div>
                <span className="text-danger">{errors.lastname && 'Last name is required.'}</span>
              </FormGroup>
              <FormGroup>
                <Label className="control-Label" htmlFor="username">
                  Username *
                </Label>
                <div className="mb-2">
                  <input
                    type="text"
                    name="username"
                    ref={register({ required: true })}
                    className="form-control"
                  />
                </div>
                <span className="text-danger">{errors.username && 'Username is required.'}</span>
              </FormGroup>
              <FormGroup>
                <Label className="control-Label" htmlFor="email">
                  Email *
                </Label>
                <div className="mb-2">
                  <input
                    type="text"
                    name="email"
                    ref={register({
                      required: true,
                      pattern: /^\S+@\S+$/i,
                    })}
                    className="form-control"
                  />
                </div>
                <span className="text-danger">{errors.email && 'Email is required.'}</span>
              </FormGroup>
              <FormGroup>
                <Label className="control-Label" htmlFor="mobile">
                  Mobile No *
                </Label>
                <div className="mb-2">
                  <input
                    type="text"
                    name="mobile"
                    ref={register({ required: true, maxLength: 11, minLength: 8 })}
                    className="form-control"
                  />
                </div>
                <span className="text-danger">
                  {errors.mobile && 'Enter a Valid mobile number.'}
                </span>
              </FormGroup>
              <FormGroup>
                <Label className="control-Label" htmlFor="age">
                  Age *
                </Label>
                <div className="mb-2">
                  <input
                    type="number"
                    name="age"
                    ref={register({ required: true, pattern: /\d+/ })}
                    className="form-control"
                  />
                </div>
                <span className="text-danger">{errors.age && 'Please enter number for age.'}</span>
              </FormGroup>
              <FormGroup>
                <Label className="control-Label" htmlFor="title">
                  Select Gender *
                </Label>
                <div className="mb-2">
                  <select name="title" className="form-control" ref={register({ required: true })}>
                    <option value="">Select Option</option>
                    <option value="Mr">Mr</option>
                    <option value="Mrs">Mrs</option>
                    <option value="Miss">Miss</option>
                  </select>
                </div>
                <span className="text-danger">{errors.title && 'Please select value.'}</span>
              </FormGroup>
              <FormGroup>
                <Label>Are you a developer?</Label>
                <br />
                <FormGroup check inline>
                  <Input
                    name="developer"
                    type="radio"
                    value="Yes"
                    ref={register({ required: true })}
                  />
                  <Label check>Yes</Label>
                </FormGroup>
                <FormGroup check inline>
                  <Input
                    name="developer"
                    type="radio"
                    value="No"
                    ref={register({ required: true })}
                  />
                  <Label check>No</Label>
                </FormGroup>
                {/* <FormGroup>
                  <Label>
                    <input
                      name="developer"
                      type="radio"
                      value="Yes"
                      ref={register({ required: true })}
                    />{' '}
                    Yes
                  </Label>

                  <Label className="ml-3">
                    <input
                      name="developer"
                      type="radio"
                      value="No"
                      ref={register({ required: true })}
                    />{' '}
                    No
                  </Label>
                </FormGroup> */}
                <span className="text-danger">{errors.developer && 'Please select value.'}</span>
              </FormGroup>
              <FormGroup>
                <Button className="button btn-info" type="submit">
                  Submit
                </Button>
              </FormGroup>
            </Form>
            <hr />
            <h4 className="mt-5">Check Data after form submit</h4>
            <ListGroup>
              <ListGroupItem>Firstname: {Formvalue.firstname}</ListGroupItem>
              <ListGroupItem>Lirstname: {Formvalue.lastname}</ListGroupItem>
              <ListGroupItem>Username: {Formvalue.username}</ListGroupItem>
              <ListGroupItem>Age: {Formvalue.age}</ListGroupItem>
              <ListGroupItem>Email Id: {Formvalue.email}</ListGroupItem>
              <ListGroupItem>Mobile No: {Formvalue.mobile}</ListGroupItem>
              <ListGroupItem>Gender: {Formvalue.title}</ListGroupItem>
              <ListGroupItem>Are you developer?: {Formvalue.developer}</ListGroupItem>
            </ListGroup>
          </ComponentCard>
        </Col>
      </Row>
    </>
  );
};

export default FormValidate;
